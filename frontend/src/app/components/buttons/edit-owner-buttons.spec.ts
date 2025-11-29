import { EditOwnerButtons } from '#components/buttons';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('EditOwnerButtons', () => {
  let component: EditOwnerButtons;
  let fixture: ComponentFixture<EditOwnerButtons>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditOwnerButtons],
    }).compileComponents();

    fixture = TestBed.createComponent(EditOwnerButtons);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
