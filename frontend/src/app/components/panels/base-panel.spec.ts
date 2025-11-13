import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BasePanel } from './base-panel';

describe('BasePanel', () => {
  let component: BasePanel;
  let fixture: ComponentFixture<BasePanel>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BasePanel]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BasePanel);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
