import { ViewOwnerForm } from '#components/forms';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('ViewOwnerForm', () => {
  let component: ViewOwnerForm;
  let fixture: ComponentFixture<ViewOwnerForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewOwnerForm],
    }).compileComponents();

    fixture = TestBed.createComponent(ViewOwnerForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
